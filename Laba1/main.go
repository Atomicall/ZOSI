package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"

	_ "github.com/Atomicall/ZOSI/Laba1/packages/imageFilter"
	imageNeg "github.com/Atomicall/ZOSI/Laba1/packages/imagePerElemProccessing"
	"gocv.io/x/gocv"
)

func main() {
	var (
		foundImageMap = make(map[string]string)
		newImages     = make(map[string]gocv.Mat)
		window        = gocv.NewWindow("Laba1")
		image         = gocv.NewMat()
		imgDir        = "images"
	)
	defer window.Close()
	defer image.Close()
	exec, err := os.Executable()
	if err != nil {
		fmt.Errorf("main.go %T", err.Error())
	}
	filepath.Walk(imgDir, func(path string, fileInfo os.FileInfo, err error) error {
		if !fileInfo.IsDir() {
			foundImageMap[fileInfo.Name()] = path
		}
		return nil
	})

	prefix := "new_"
	for name, path := range foundImageMap {
		newName := prefix + name
		newImages[newName] = imageNeg.ConvertToNegative(gocv.IMRead(path, gocv.IMReadColor))
		err := gocv.IMWrite(filepath.Join(filepath.Dir(exec), imgDir, "output", newName), newImages[newName])
		if err != true {
			fmt.Printf("Error writing image")
		}
	}

	input := bufio.NewScanner(os.Stdin)
	for name, _ := range newImages {
		for s := ""; input.Scan(); s = input.Text() {
			window.IMShow(newImages[name])
			window.WaitKey(1)
			if s == "#q" {
				break
			}
		}
	}
}
