package imagePerElemProccessing

import (
	"fmt"

	"gocv.io/x/gocv"
)

func ConvertToNegative(image gocv.Mat) gocv.Mat {
	var (
		intence   uint8 = 255
		rows            = image.Rows()
		cols            = image.Cols()
		channels        = image.Channels()
		dataImage       = image.ToBytes()
	)
	for row := 0; row < rows; row++ {
		for col := 0; col < cols; col++ {
			for ch := 0; ch < channels; ch++ {
				idx := row*cols + col + ch
				dataImage[idx] = intence - dataImage[idx]
			}
		}
	}
	negativeImage, err := gocv.NewMatFromBytes(rows, cols, image.Type(), dataImage)
	if err != nil {
		fmt.Printf("%T", err.Error())
	}
	return negativeImage
}
