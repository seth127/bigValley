shinyUI(fluidPage(
  titlePanel("title panel"),
  
  sidebarLayout(
    sidebarPanel( "sidebar panel",
                  radioButtons("statPick", " type:",
                               c("Full List" = "full",
                                 "Critter Stats" = "critters",
                                 "Counts" = "numbers"))),
    mainPanel("main panel",
              plotOutput("thePlot"))
  )
))