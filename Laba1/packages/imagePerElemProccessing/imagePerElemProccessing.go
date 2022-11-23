package imagePerElemProccessing

import (
	"fmt"

	"gocv.io/x/gocv"
)

func ConvertToNegative(image gocv.Mat) gocv.Mat {
	var (
		intence       uint8 = 0xff
		rows                = image.Rows()
		cols                = image.Cols()
		negativeImage       = gocv.NewMatWithSize(rows, cols, image.Type())
		size                = image.ElemSize() * rows * cols
	)

	data, err := image.DataPtrUint8()
	if err != nil {
		fmt.Printf("\t[ERORR] - imagePerElemProccessing.go(ConvertToNegative) - can't get image data\n")
	}
	result, err2 := negativeImage.DataPtrUint8()
	if err2 != nil {
		fmt.Printf("\t[ERORR] - imagePerElemProccessing.go(ConvertToNegative) - can't get image data\n")
	}
	for i := 0; i < size; i++ {
		result[i] = intence - data[i]
	}

	return negativeImage
}
