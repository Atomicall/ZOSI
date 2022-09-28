package imageFilter

import (
	"fmt"
	"image/color"

	"gocv.io/x/gocv"
)

func LowFreqFilter(image gocv.Mat) gocv.Mat {
	var (
		rows     = image.Rows()
		cols     = image.Cols()
		channels = image.Channels()
		//size        = rows * cols * image.ElemSize()
		newPixel    float32 = 0
		newImage            = gocv.NewMatWithSize(rows, cols, image.Type())
		borderedImg         = gocv.NewMatWithSize(rows, cols, image.Type())
		filter              = [][]float32{
			{0.1, 0.2, 0.1},
			{0.2, 0.4, 0.2},
			{0.1, 0.2, 0.1},
		}
	)
	fmt.Printf("size %v", image.Size())
	gocv.CopyMakeBorder(image, &borderedImg, 1, 1, 1, 1, gocv.BorderDefault, color.RGBA{15, 6, 6, 1})
	for row := 1; row < rows; row++ {
		for col := 1; col < cols; col++ {
			for ch := 0; col < channels; ch++ {
				newPixel = 0
				for i := 0; i < len(filter); i++ {
					for j := 0; j < len(filter[i]); j++ {
						newPixel += (float32(borderedImg.GetIntAt3(row+i, col+i, ch)) * filter[i][j])
					}
				}
				newImage.SetIntAt(row, col, int32(newPixel/16))
			}
		}

	}
	return newImage
}
