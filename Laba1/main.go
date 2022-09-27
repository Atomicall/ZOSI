package main

import (
	"flag"
	"fmt"

	"gocv.io/x/gocv"
)

func main() {
	flag.Usage = func() {
		fmt.Println("How to run:\n\tlaba1COSI [-flags] [image1.jpg] [image2.jpg]")
		flag.PrintDefaults()
	}

	webcam, _ := gocv.OpenVideoCapture(0)
	defer webcam.Close()

	window := gocv.NewWindow("Hello")
	defer window.Close()

	imageFilter.printStatus()
	img := gocv.NewMat()

	for {
		webcam.Read(&img)
		window.IMShow(img)
		window.WaitKey(1)
	}
}
