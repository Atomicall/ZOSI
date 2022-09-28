package helpFuncs

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	"gocv.io/x/gocv"
)

func ShowImages(imageMap map[string]gocv.Mat) {
	fmt.Printf("Starting images presentation....\n")
	window := gocv.NewWindow("Laba1")
	defer window.Close()
	for name, _ := range imageMap {
		fmt.Printf("\tImage : %s\n", name)
		window.IMShow(imageMap[name])
		window.WaitKey(5 * int(time.Second))
	}
}

func ShowImagesWithPaths(imageMap map[string]string) {
	fmt.Printf("Starting images presentation....\n")
	window := gocv.NewWindow("Laba1")
	defer window.Close()
	for name, _ := range imageMap {
		fmt.Printf("\tImage : %s\n", name)
		window.IMShow(gocv.IMRead(imageMap[name], gocv.IMReadAnyColor))
		window.WaitKey(5 * int(time.Second))
	}
}

func ProccessImageWithFunc(imageMap map[string]string,
	fn func(image gocv.Mat) gocv.Mat, outDir string, prefix string) (map[string]gocv.Mat, map[string]string) {

	var newImages = make(map[string]gocv.Mat)
	var newImagesPaths = make(map[string]string)

	fmt.Printf("Starting image processing\n")
	for name, path := range imageMap {
		fmt.Printf("\tProcessing image : %s...\n", name)
		newName := prefix + name
		newImages[newName] = fn(gocv.IMRead(path, gocv.IMReadColor))

		fmt.Printf("\t\tSuccesfully proccesed image!\n")
		img, errors := os.Create(filepath.Join(".\\", outDir, newName))
		if errors != nil {
			fmt.Printf("\t\t[ERROR] - %v\n", errors.Error())
			continue
		}
		defer img.Close()

		fmt.Printf("\t\tSaving as %s...\n", newName)
		newImagesPaths[newName] = filepath.Join(outDir, newName)
		err := gocv.IMWrite(newImagesPaths[newName], newImages[newName])
		if !err {
			fmt.Println("[ERROR] - Error writing image")
			continue
		}
		fmt.Printf("\t\tdone!\n")
	}
	return newImages, newImagesPaths
}
