def highlight(element, color, border):
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    apply_style("border: {0}px solid {1};".format(border, color))