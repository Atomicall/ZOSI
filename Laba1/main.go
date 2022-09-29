package main

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/Atomicall/ZOSI/Laba1/packages/helpFuncs"
	"github.com/Atomicall/ZOSI/Laba1/packages/histogram"
	"github.com/Atomicall/ZOSI/Laba1/packages/imageFilter"
	_ "github.com/Atomicall/ZOSI/Laba1/packages/imageFilter"
	"github.com/Atomicall/ZOSI/Laba1/packages/imagePerElemProccessing"
)

func main() {
	var (
		foundImagePathsMap = make(map[string]string)
		imgDir             = "images"
		outDir             = "out"
		filter             = [][]uint8{
			{1, 1, 1, 1, 1},
			{1, 1, 1, 1, 1},
			{1, 1, 1, 1, 1},
			{1, 1, 1, 1, 1},
			{1, 1, 1, 1, 1},
		}
	)

	fmt.Printf("Looking for images in <images> folder....\n")
	filepath.Walk(imgDir, func(path string, fileInfo os.FileInfo, err error) error {
		if !fileInfo.IsDir() {
			foundImagePathsMap[fileInfo.Name()] = path
			fmt.Printf("\tFound image : %s\n", fileInfo.Name())
		}
		return nil
	})
	histogram.MakeAndSaveHistograms(foundImagePathsMap, outDir)
	helpFuncs.ShowImagesWithPaths(foundImagePathsMap)

	negImages, negImagesPath := helpFuncs.ProccessImageWithFunc(foundImagePathsMap, imagePerElemProccessing.ConvertToNegative, outDir, "negative_")
	histogram.MakeAndSaveHistograms(negImagesPath, outDir)
	helpFuncs.ShowImages(negImages)

	filteredImages, filteredImagesPaths := helpFuncs.ProccessImageWithFilter(foundImagePathsMap, imageFilter.LowFreqFilter, filter, outDir, "filtered_")
	histogram.MakeAndSaveHistograms(filteredImagesPaths, outDir)
	helpFuncs.ShowImages(filteredImages)

	fmt.Printf("Ending of the program...")
}
