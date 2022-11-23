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

func ShowImagesWithPaths(imagePathsMap map[string]string) {
	fmt.Printf("Starting images presentation....\n")
	window := gocv.NewWindow("Laba1")
	defer window.Close()
	for name, _ := range imagePathsMap {
		fmt.Printf("\tImage : %s\n", name)
		window.IMShow(gocv.IMRead(imagePathsMap[name], gocv.IMReadAnyColor))
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
		start := time.Now()

		newName := prefix + name
		newImages[newName] = fn(gocv.IMRead(path, gocv.IMReadColor))

		fmt.Printf("\t\tSuccesfully proccesed image!\n")
		img, errors := os.Create(filepath.Join(".\\", outDir, newName))
		if errors != nil {
			fmt.Printf("\t\t[ERROR] - %v\n", errors.Error())
			continue
		}
		defer img.Close()

		fmt.Printf("\t\tSaving as %s...", newName)
		newImagesPaths[newName] = filepath.Join(outDir, newName)
		err := gocv.IMWrite(newImagesPaths[newName], newImages[newName])
		if !err {
			fmt.Println("[ERROR] - Error writing image")
			continue
		}
		fmt.Printf("\tdone!\n\t\tElapsed : %v \n", time.Since(start))
	}
	return newImages, newImagesPaths
}

func ProccessImageWithFilter(imageMap map[string]string,
	fn func(image gocv.Mat, filter [][]uint8) gocv.Mat, filter [][]uint8, outDir string, prefix string) (map[string]gocv.Mat, map[string]string) {

	var (
		newImages      = make(map[string]gocv.Mat)
		newImagesPaths = make(map[string]string)
	)
	fmt.Printf("Starting image processing\n")
	for name, path := range imageMap {
		fmt.Printf("\tProcessing image : %s...\n", name)
		start := time.Now()

		newName := prefix + name
		newImages[newName] = fn(gocv.IMRead(path, gocv.IMReadColor), filter)

		fmt.Printf("\t\tSuccesfully proccesed image!\n")
		img, errors := os.Create(filepath.Join(".\\", outDir, newName))
		if errors != nil {
			fmt.Printf("\t\t[ERROR] - %v\n", errors.Error())
			continue
		}
		defer img.Close()

		fmt.Printf("\t\tSaving as %s...", newName)
		newImagesPaths[newName] = filepath.Join(outDir, newName)
		err := gocv.IMWrite(newImagesPaths[newName], newImages[newName])
		if !err {
			fmt.Println("[ERROR] - Error writing image")
			continue
		}
		fmt.Printf("\tdone!\n\t\tElapsed : %v \n", time.Since(start))
	}
	return newImages, newImagesPaths
}
