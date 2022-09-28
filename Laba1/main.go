package main

import (
	"fmt"
	"os"
	"path/filepath"

	helpfuncs "github.com/Atomicall/ZOSI/Laba1/packages/helpFuncs"
	_ "github.com/Atomicall/ZOSI/Laba1/packages/imageFilter"
	"github.com/Atomicall/ZOSI/Laba1/packages/imagePerElemProccessing"
)

func main() {
	var (
		foundImageMap = make(map[string]string)
		imgDir        = "images"
		outDir        = "out"
	)

	fmt.Printf("Looking for images in <images> folder....\n")
	filepath.Walk(imgDir, func(path string, fileInfo os.FileInfo, err error) error {
		if !fileInfo.IsDir() {
			foundImageMap[fileInfo.Name()] = path
			fmt.Printf("\tFound image : %s\n", fileInfo.Name())
		}
		return nil
	})
	helpfuncs.ShowImagesWithPaths(foundImageMap)
	negImages := helpfuncs.ProccessImageWithFunc(foundImageMap, imagePerElemProccessing.ConvertToNegative, outDir)
	helpfuncs.ShowImages(negImages)
	fmt.Printf("Ending of the program...")
}
