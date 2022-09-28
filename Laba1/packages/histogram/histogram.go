package histogram

import (
	"fmt"
	"image/color"
	"path/filepath"

	"gocv.io/x/gocv"
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/vg"
)

func MakeAndSaveHistograms(imageMap map[string]string, outDir string) {
	var (
		plotMap = make(map[string]*plot.Plot)
	)
	fmt.Printf("Making Historgrams for images:\n")
	for name, path := range imageMap {
		fmt.Printf("\tHistogram for image : %s", name)
		plotMap[name] = makeHistogramPlot(gocv.IMRead(path, gocv.IMReadColor), "Histogram for "+name)
		if err := plotMap[name].Save(5*vg.Inch, 5*vg.Inch, filepath.Join(outDir, "histogram_"+name)); err != nil {
			panic(err)
		}
		fmt.Printf("\tdone!\n")
	}

}

func makeHistogramPlot(image gocv.Mat, title string) *plot.Plot {
	var (
		size   = image.ElemSize() * image.Cols() * image.Rows()
		values plotter.Values
	)
	imgData, err := image.DataPtrUint8()
	if err != nil {
		panic(err)
	}
	plt := plot.New()
	for i := 0; i < size; i++ {
		values = append(values, float64(imgData[i]))
	}
	plt.Title.Text = title
	hist, err := plotter.NewHist(values, 255)
	if err != nil {
		panic(err)
	}
	hist.Color = color.RGBA{255, 0, 0, 0}
	plt.Add(hist)
	return plt
}
