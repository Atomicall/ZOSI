package imageFilter

import (
	"image/color"

	"gocv.io/x/gocv"
)

func LowFreqFilter(image gocv.Mat, filter [][]uint8) gocv.Mat {
	var (
		rows     = image.Rows()
		cols     = image.Cols()
		channels = image.Channels()
		//size        = image.Total()
		newPixel    uint32 = 0
		imType             = image.Type()
		elemSize           = image.ElemSize()
		newImage           = gocv.NewMatWithSize(rows, cols, imType)
		borderedImg        = gocv.NewMatWithSize(rows, cols, imType)

		startingPixel = len(filter[0]) / 2 * elemSize
	)
	sum := func(filter [][]uint8) uint8 {
		var res uint8 = 0
		for i := 0; i < len(filter); i++ {
			for j := 0; j < len(filter[i]); j++ {
				res += filter[i][j]
			}
		}
		return res
	}
	divider := sum(filter)
	gocv.CopyMakeBorder(image, &borderedImg,
		startingPixel, startingPixel, startingPixel, startingPixel, gocv.BorderDefault, color.RGBA{0, 0, 0, 0})
	for row := 1; row < rows; row++ {
		for col := startingPixel; col < cols; col++ {
			for ch := 0; ch < channels; ch++ {
				newPixel = 0
				for i := 0; i < len(filter); i++ {
					for j := 0; j < len(filter[i]); j++ {
						newPixel += uint32(borderedImg.GetUCharAt((row+i-1), (col*elemSize+j*elemSize-startingPixel+ch)) * filter[i][j] / divider)
					}
					if newPixel > 255 {
						newPixel = 255
					}
					newImage.SetUCharAt(row, col*elemSize+ch, uint8(newPixel))
				}

			}
		}

	}
	return newImage
}
