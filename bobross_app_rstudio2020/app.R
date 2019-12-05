library(shiny)
library(png)
library(shinyWidgets)
library(shinyjs)
library(tm)
library(arules)
library(arulesViz)
library(stringr)
library(ggplot2)
library(shinythemes)
library(NLP)
library(class)
library(openNLP)

dat <- read.csv("./bob-ross.csv")
source("funcs.R")
df <- read.csv("by_season.csv")
col1 <- read.csv("col1.csv")[3:18]
col2 <- read.csv("col2.csv")[3:8]
seasons <- reshape2::melt(df, id.var='SEASON')
var_opt = unique(seasons$variable)
var_opt_2 = colnames(col1)[1:8]
var_opt_3 = colnames(col1)[9:16]
var_opt_4 = colnames(col2)

# Define UI for application
ui <- fluidPage(
  theme = shinytheme("flatly"),
  headerPanel("Painting by the Numbers: Bob Ross"),
  tabsetPanel(
    tabPanel("Painting Creator",
  fluidRow(column(12,h3("Create your own Bob Ross painting"))),
  setBackgroundImage(
    src = "www/bob.png"
  ),
  
  fluidRow(
    column(2, wellPanel(
      selectInput("sky", "Sky:",
                   c("clouds", "sunset", "mountains", "snow")),
      selectInput("ground", "Ground:",
                   c("grass", "ocean", "river", "lake")),
      selectInput("frame", "Frame:",
                   c("rectangular", "circle", "oval", "seashell", "window", "wood")),

      sliderInput("tree", "Number of trees", 0, 10, 0),
      checkboxInput("flowers", "Flowers", value = FALSE),
      checkboxInput("bushes", "Bushes", value = FALSE),
      checkboxInput("moon", "Moon", value = FALSE),
      checkboxInput("cabin", "Cabin", value = FALSE),
      checkboxInput("bob", "Bob Ross", value = FALSE),
      actionButton("button", "Generate title!")
    )),
    column(3,
    
           imageOutput("image1", height = "3px", width = "3px")
    ,
    
           imageOutput("image2", height = "3px", width = "3px")
    ,
          imageOutput("image5", height = "3px", width = "3px"),
          imageOutput("image3", height = "3px", width = "3px"),
          imageOutput("image9", height = "3px", width = "3px"),
          imageOutput("image4", height = "3px", width = "3px"),
          imageOutput("image8", height = "3px", width = "3px"),
          imageOutput("image7", height = "3px", width = "3px"),
          imageOutput("image6", height = "3px", width = "3px")
    ),
    column(2, offset=4,
      h1("WWBRD"),
      h6("(What Would Bob Ross Do?)"),
      h4("Bob Ross would call this..."),
      p(id='text_div',
          verbatimTextOutput("text")
      ),
      h4("Bob Ross would add..."),
      p(id='text_div',
        verbatimTextOutput("text2")
      )
    )
  )

),tabPanel("Paintings Through the Years",
           fluidRow(column(12,h3("Across seasons, how often have different elements appeared in paintings?"))),
           sidebarLayout(
             sidebarPanel(
               width = 2,
               checkboxGroupInput("var", "Element:",
                                  choices=var_opt,
                                  selected="CLOUDS")),
             mainPanel(plotOutput("plot"),h5("Note: There were a total of 13 episodes in each season."))
           )
),tabPanel("Episode Recommendations",
           fluidRow(column(12,h3("What episodes should you watch?"))),
           fluidRow(
             column(4,h4("A painting with..."),
                    span("Choose some elements & we'll pick the closest painting."),
                    fluidRow(
                      column(6,checkboxGroupInput("var2", "",
                                                  choices=var_opt_2)),
                      column(6,checkboxGroupInput("var3","", choices=var_opt_3))),
                    actionButton("choose_el", "Generate")
                    ),
             column(4,h4("Something special"),
                    span("These elements only appear in a few episodes! Choose one to get a recommendation."),
                    radioButtons("var4", "", choices=var_opt_4),
                    actionButton("choose_special", "Generate")),
             column(4,
                    h4("Surprise me!"),
                    p("Click the button to randomly choose an episode."),
                    actionButton("random", "Generate"),
                    br()
                    )
           ),
           fluidRow(
             column(6,offset=3, 
                    h3(textOutput("choose_ep"))
                    )
           )
), tabPanel("About this App",
            fluidRow(column(10, offset=1,br(),
              h5("This app was created to explore the Tidy Tuesdays Bob Ross dataset from 538. It was created by 
                Ashley Jacobson and Markelle Kelly.")
            )),
           fluidRow(
             column(4, offset=1,h3("Painting Creator"), p("The painting creator, in addition to
                    visualizing the painting you design in the style of Bob Ross, predicts the title and
                                                          other elements Bob Ross would suggest. The title is
                                                          generated based on paintings with similar backgrounds (i.e,
                                                          based on the \"sky\" and \"ground\" options). From the set of
                                                          similar paintings, we pulled out the nouns and adjectives using
                                                          the openNLP package, and generated a random noun/adjective pair.
                                                          To predict what elements Bob
                                                          Ross would add, we used the apriori algorithm to generate
                                                          association rules. We return elements x with a confidence
                                                          above 0.35 for (current elements)→(x).")
           ),
           column(4, offset=1,h3("Episode Recommendations"), p("The episode recommender offers three different
                                                               methods of getting suggestions. The first allows
                                                               users to choose elements they want to see in a painting and
                                                               performs K-Nearest-Neighbors to get the closest 
                                                               real painting. In the case of a tie, clicking the
                                                               button multiple times will return multiple different 
                                                               episodes. The second column includes several elements 
                                                               that only appear in a few (less than 10) episodes.
                                                               Clicking the button returns a random episode with 
                                                               the chosen element. Finally, the \"Surprise me!\"
                                                               section will generate a completely random episode."))
           )
)))

# Define server logic required to draw the image
server <- function(input, output) {
  output$plot <- renderPlot({
    dat <- subset(seasons, seasons$variable %in% input$var)
    ggplot(data=dat, aes(x=SEASON,y=value)) + geom_line(aes(color=variable),size=1.2) +
      labs(title="Painting Feature Popularity Over Time", x="Season",y="Number of Uses",color="Features") +
      scale_fill_brewer(palette = "Set1") +
      theme_bw()
  })
  output$text <- renderText({paste(title_word(input$sky))})
  observeEvent(input$button, {
    output$text <- renderText({paste(title_word(input$sky))})
  })
  output$choose_ep <- renderText({paste("")})
  observeEvent(input$random, {
    output$choose_ep <- renderText({paste(surprise())})
  })
  observeEvent(input$choose_el, {
    output$choose_ep <- renderText({paste(my_knn(isolate(input$var2),isolate(input$var3)))})
  })
  observeEvent(input$choose_special, {
    output$choose_ep <- renderText({paste(special(isolate(input$var4)))})
  })
  output$text2 <- renderText({
    sky <- input$sky
    if (input$sky == "sunset") {
      sky <- "SUN"
    }
    inputs <- c(str_to_upper(sky),str_to_upper(input$ground))
    if (input$ground == "river") {
      inputs <- c(inputs, "GRASS")
      if (input$bushes != TRUE) {
        inputs <- c(inputs, "BUSHES")
      }
    }
    if (input$sky == "mountains" | input$sky == "snow") {
      inputs <- c(inputs,"SNOWY_MOUNTAIN","MOUNTAIN","CLOUDS","WINTER")
      if (input$tree == 0) {
        inputs <- c(inputs,"TREES")
      }
    }
    if (input$sky == "mountains") {
      inputs <- c(inputs, "SNOW")
    }
    if (input$sky == "snow") {
      inputs <- c(inputs, "MOUNTAINS")
    }
    if (input$tree > 0) {
      inputs <- c(inputs,"TREES")
    }
    if (input$flowers == TRUE) {
      inputs <- c(inputs,"FLOWERS")
    }
    if (input$moon == TRUE) {
      inputs <- c(inputs, "MOON")
    }
    if (input$bushes == TRUE) {
      inputs <- c(inputs, "BUSHES")
    }
    if (input$cabin == TRUE) {
      inputs <- c(inputs, "CABIN", "STRUCTURE")
    }
    if (!is.null(input$frame)) {
      if (input$frame == "wood") {
        inputs <- c(inputs, "WOOD_FRAMED")
      } else {
        new <- paste(str_to_upper(input$frame), "_FRAME",sep="")
        inputs <- c(inputs, new)
      }
    }
    return(paste(run_apriori(inputs),collapse="\n"))
  })
  output$image1 <- renderImage({
    if (is.null(input$ground))
      return(NULL)
    
    if (input$ground == "ocean") {
      return(list(
        src = "www/ocean.png",
        contentType = "image/png",
        alt = "ocean"
      ))
    } else if (input$ground == "grass") {
      return(list(
        src = "www/grass.png",
        filetype = "image/png",
        alt = "grass"
      ))
    } else if (input$ground == "river") {
      return(list(
        src = "www/river.png",
        filetype = "image/png",
        alt = "river"
      ))
    }else if (input$ground == "lake") {
      return(list(
        src = "www/lake.png",
        filetype = "image/png",
        alt = "lake"
      ))
    }
    
  }, deleteFile = FALSE)
  
  output$image2 <- renderImage({
    if (is.null(input$sky))
      return(NULL)
    
    if (input$sky == "clouds") {
      return(list(
        src = "www/clouds.png",
        contentType = "image/png",
        alt = "clouds"
      ))
    } else if (input$sky == "sunset") {
      return(list(
        src = "www/sunset.png",
        filetype = "image/png",
        alt = "sunset"
      ))
    } else if (input$sky == "mountains") {
      return(list(
        src = "www/mountains.png",
        filetype = "image/png",
        alt = "mountains"
      ))
    } else if (input$sky == "snow") {
      return(list(
        src = "www/snow.png",
        filetype = "image/png",
        alt = "snow"
      ))
    }
    
  }, deleteFile = FALSE)
  
  
  output$image3 <- renderImage({
    if (is.null(input$tree))
      return(NULL)
    
    if (input$tree == 0) {
      return(list(
        src = "www/none.png",
        contentType = "image/png",
        alt = "none"
      ))
    } else {
      f <- paste("www/tree", input$tree, ".png", sep = '')
      return(list(
        src = f,
        contentType = "image/png",
        alt = "tree"
      ))
    }  }, deleteFile = FALSE)
  
  output$image4 <- renderImage({
    if (is.null(input$flowers))
      return(NULL)
    
    if (input$flowers == TRUE) {
      return(list(
        src = "www/flowers.png",
        contentType = "image/png",
        alt = "flowers"
      ))
    } else {
      return(list(
        src = "www/none.png",
        contentType = "image/png",
        alt = "none"
      ))
    }  }, deleteFile = FALSE)
  
  output$image8 <- renderImage({
    if (is.null(input$bushes))
      return(NULL)
    
    if (input$bushes == TRUE) {
      return(list(
        src = "www/bushes.png",
        contentType = "image/png",
        alt = "bushes"
      ))
    } else {
      return(list(
        src = "www/none.png",
        contentType = "image/png",
        alt = "none"
      ))
    }  }, deleteFile = FALSE)
  
  
  output$image5 <- renderImage({
    if (is.null(input$moon))
      return(NULL)
    
    if (input$moon == TRUE) {
      return(list(
        src = "www/moon.png",
        contentType = "image/png",
        alt = "moon"
      ))
    } else {
      return(list(
        src = "www/none.png",
        contentType = "image/png",
        alt = "none"
      ))
    }  }, deleteFile = FALSE)
  
  
  output$image6 <- renderImage({
    if (is.null(input$bob))
      return(NULL)
    
    if (input$bob == TRUE) {
      return(list(
        src = "www/bob.png",
        contentType = "image/png",
        alt = "bob"
      ))
    } else {
      return(list(
        src = "www/none.png",
        contentType = "image/png",
        alt = "none"
      ))
    }  }, deleteFile = FALSE)
  
  
  output$image9 <- renderImage({
    if (is.null(input$cabin))
      return(NULL)
    
    if (input$cabin == TRUE) {
      return(list(
        src = "www/cabin.png",
        contentType = "image/png",
        alt = "cabin"
      ))
    } else {
      return(list(
        src = "www/none.png",
        contentType = "image/png",
        alt = "none"
      ))
    }  }, deleteFile = FALSE)
  
  
  output$image7 <- renderImage({
    if (is.null(input$frame))
      return(NULL)
    
    if (input$frame == "rectangular") {
      return(list(
        src = "www/none.png",
        contentType = "image/png",
        alt = "none"
      ))
    } else if (input$frame == "circle") {
      return(list(
        src = "www/circle_frame.png",
        filetype = "image/png",
        alt = "circle frame"
      ))
    } else if (input$frame == "oval") {
      return(list(
        src = "www/oval_frame.png",
        filetype = "image/png",
        alt = "oval frame"
      ))
    } else if (input$frame == "seashell") {
      return(list(
        src = "www/seashell_frame.png",
        filetype = "image/png",
        alt = "seashell frame"
      ))
    } else if (input$frame == "window") {
      return(list(
        src = "www/window_frame.png",
        filetype = "image/png",
        alt = "window frame"
      ))
    } else if (input$frame == "wood") {
      return(list(
        src = "www/wood_frame.png",
        filetype = "image/png",
        alt = "wood frame"
      ))
    }
    
  }, deleteFile = FALSE)
  
  
}

# Run the application 
shinyApp(ui = ui, server = server)

