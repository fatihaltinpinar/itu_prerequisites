package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"golang.org/x/net/html/charset"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}


var code_list = []string{	"ATA", "AKM", "BED", "BIL", "BIO", "BLG", "BUS", "CAB", "CEV", "CHZ", "CIE",
							"CMP", "COM", "DEN", "DFH", "DNK", "DUI", "EAS", "ECO", "ECN", "EHB", "EHN",
							"EKO", "ELE", "ELH", "ELK", "END", "ENR", "ESL", "ETH", "ETK", "EUT", "FIZ",
							"GED", "GEM", "GEO", "GID", "GMI", "GSB", "GUV", "HUK", "HSS", "ICM", "ILT",
							"IML", "ING", "INS", "ISE", "ISL", "ISH", "ITB", "JDF", "JEF", "JEO", "KIM",
							"KMM", "KMP", "KON", "MAD", "MAK", "MAL", "MAR", "MAT", "MCH", "MEK", "MEN",
							"MET", "MIM", "MOD", "MRE", "MRT", "MTO", "MTH", "MTM", "MTR", "MST", "MUH",
							"MUK", "MUT", "MUZ", "NAE", "NTH", "PAZ", "PEM", "PET", "PHE", "PHY", "RES",
							"SBP", "SES", "STA", "STI", "TDW", "TEB", "TEK", "TEL", "TER", "TES", "THO",
							"TUR", "UCK", "UZB", "YTO", "YZV",
}


type Class struct {
	Lecture_name string
	Lecture_preq []string
}

var classes map[string]Class

func main() {
	classes = make(map[string]Class)

	APIURL := "http://www.sis.itu.edu.tr/TR/ogrenci/lisans/onsartlar/onsartlar.php"
	//APIURL := "https://www.sis.itu.edu.tr/EN/student/undergraduate/prerequisites/prerequisites.php"


	done := make(chan int)

	class_ch := make(chan string, 1)
	name_ch := make(chan string, 1)
	deps_ch := make(chan string, 1)
	go func() {
		for class := range class_ch {

			deps := <-deps_ch
			name := <-name_ch

			deps = strings.ReplaceAll(deps, "MIN BL", "")
			deps = strings.ReplaceAll(deps, "MIN DC", "")
			deps = strings.ReplaceAll(deps, "MIN DD", "")
			deps = strings.ReplaceAll(deps, "MIN CC", "")
			deps = strings.ReplaceAll(deps, "MIN BB", "")
			deps = strings.ReplaceAll(deps, "Yok", "")
			deps = strings.ReplaceAll(deps, "Diğer Şartlar", "")
			deps = strings.TrimSpace(deps)

			ve := strings.Split(deps, "ve ")
			preq := []string{}

			for _, s := range ve {
				veya := strings.Split(s, "veya ")
				for i := range veya {
					veya[i] = strings.Trim(veya[i], "()")
					veya[i] = strings.TrimSpace(veya[i])
					if len(veya[i]) <= 12 && len(veya[i]) > 1 {
						preq = append(preq, veya[i])
					} else {
						//fmt.Print(veya[i])
					}
				}
			}

			if _, ok := classes[class]; ok {
				//classes[class] = append(classes[class], []string{deps})
				panic("Fix here sometime")
			} else {
				classes[class] = Class{
					Lecture_name: name,
					Lecture_preq: preq,
				}
			}
		}
		done <- 0
	}()


	for _, code := range code_list{
		res, err := http.PostForm(APIURL, url.Values{
			"derskodu": {code},
		})

		fmt.Println(code)

		check(err)
		defer res.Body.Close()

		if res.StatusCode != 200 {
			log.Fatalf("status code error: %d %s", res.StatusCode, res.Status)
		}

		reader, err := charset.NewReaderLabel("windows-1254", res.Body)
		check(err)

		// Load the HTML document
		doc, err := goquery.NewDocumentFromReader(reader)
		if err != nil {
			log.Fatal(err)
		}

		doc.Find(".table > tbody:nth-child(2) > tr").Each(func(i int, s *goquery.Selection) {
			s.Find("td").Each(func(i int, s *goquery.Selection) {
				sec := s.Text()
				switch i {
				case 0:
					class_ch <- sec
				case 1:
					name_ch <- sec
				case 2:
					deps_ch <- sec
				}
			})
		})
	}

	close(class_ch)
	close(deps_ch)
	close(name_ch)


	<-done

	jsonString, err := json.MarshalIndent(classes,"", "    ")

	check(err)


	f, err := os.Create("./lectures.json")
	check(err)

	defer f.Close()

	w := bufio.NewWriter(f)
	n4, err := w.WriteString(string(jsonString))
	check(err)
	fmt.Printf("wrote %d bytes\n", n4)

	w.Flush()
}
