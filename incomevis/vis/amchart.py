import IPython

def getInteractive(k = 'decile', toState = False, outputHTML = False,
                   input_path = '', output_path = ''):
  #Missing files - Need to fix
  if k == 'decile':
    if(not toState): html1 = open(input_path + 'html1_d_year.txt', 'r')
    else: html1 = open(input_path + 'html1_p_state.txt', 'r')
  elif k == 'percentile':
    if (not toState): html1 = open(input_path + 'html1_p_year.txt', 'r')
    else: html1 = html1 = open(input_path + 'html1_p_state.txt', 'r')
  html2 = open(input_path + 'html2.txt', 'r')

  #Need to fix 
  json = open(input_path + 'decile_year_amchart_js_RHHINCOME1976.js','r')
  AmChart = html1.read() + json.read() + html2.read()
  if outputHTML:
    with open(output_path + 'decile_year_amchart_html_RHHINCOME1976.html', 'w') as outfile:
      outfile.write(AmChart)
  return IPython.display.HTML(data = AmChart)