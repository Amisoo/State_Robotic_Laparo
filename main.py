from plot import plot
import os
import glob
import webbrowser


def main(path):
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    # html page
    html = open('Timeline_state.html', 'w')
    html.write(
        '<html><head><title> Timeline state   '
        '  </title> </head> <div> <center>  <h1 style="font-family: Arial"> State of Laparo, Motion and Ready for operation  </h1> </center> '
        '  </div>     </body></html>')

    html.close()

    # loop over the list of csv files
    for f in csv_files:
        fig = plot(f)
        # transfer of plot to html file
        with open('Timeline_state.html', 'a') as d:
            d.write("<center>")
            d.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
            d.write("</center>")
    # launch of page
    webbrowser.open('Timeline_state.html')


main(r"F:\csv\2023_08_10")