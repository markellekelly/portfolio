library(ggplot2)
library(scales)
library(shiny)
df <- read.csv("featuresdf.csv")
colnames(df)<- c("id","name","artists","Danceability","Energy","key","Loudness","Mode","Speechiness","Acousticness","Instrumental",
                 "Liveness","Valence","Tempo","Duration","time_signature","Genre","Sex") 
df$Mode <- factor(df$Mode, levels=c(0,1), labels=c("Minor","Major"))
library(DT)

mean = sapply(df[,c('Danceability','Energy','Loudness','Speechiness',
                            'Acousticness','Instrumental','Liveness','Valence',
                            'Tempo','Duration')], mean)
sd = sapply(df[,c('Danceability','Energy','Loudness','Speechiness',
                   'Acousticness','Instrumental','Liveness','Valence',
                   'Tempo','Duration')], sd)
min = sapply(df[,c('Danceability','Energy','Loudness','Speechiness',
             'Acousticness','Instrumental','Liveness','Valence',
             'Tempo','Duration')], min)
max = sapply(df[,c('Danceability','Energy','Loudness','Speechiness',
             'Acousticness','Instrumental','Liveness','Valence',
             'Tempo','Duration')], max)

quant_summary = t(data.frame(rbind(mean, sd, min, max)))

genre_num = (data.frame(tapply(df$id, df$Genre, length)))
names(genre_num) = 'count'

sex_num = (data.frame(tapply(df$id, df$Sex, length)))
names(sex_num) = 'count'

mode_num =  (data.frame(tapply(df$id, df$Mode, length)))
names(mode_num) = 'count'

ui <- fluidPage(
  headerPanel("Exploration of Top Spotify Songs 2017"),
  tabsetPanel(
    tabPanel("Qualitative Variables by Genre",
             titlePanel("Qualitative Variables by Genre"),
             sidebarLayout(
               sidebarPanel(
                 width = 3,
                 checkboxGroupInput("genre", "Genre:",
                                    choices=c("Pop","Latino","Dance","Hip-Hop/Rap","Alternative","R&B/Soul"),
                                    selected="Pop"),
                 radioButtons("x", "Variable to Plot:", choices = c("Danceability", "Energy", "Loudness", "Speechiness",
                                                                   "Acousticness", "Liveness", "Valence"))),
               mainPanel(plotOutput("plot"))
             )
    ),
    tabPanel("Artists by Genre",
             titlePanel("Artists by Genre"),
             sidebarLayout(
               sidebarPanel(
                 width = 3,
                 checkboxGroupInput("genres", "Genre:", 
                                    choices=c("Pop","Latino","Dance",
                                              "Hip-Hop/Rap","Soundtrack",
                                              "Alternative","R&B/Soul","Country"),
                                    selected="Pop"),
                 checkboxGroupInput("sex", "Sex:", 
                                    choices=c("female","male"), selected = c("female","male"))),
               
               mainPanel(plotOutput("plot1"), plotOutput("plotgender"))
             )
    ),
    
    tabPanel("Regression",
             titlePanel("Regression"),
             sidebarLayout(
               sidebarPanel(
                 fluidRow(
                   column(6,
                          radioButtons("xvar", "X Variable:",
                                       choiceValues=c("Danceability","Energy","Tempo","Duration",
                                                      "Loudness","Speechiness","Valence",
                                                      "Acousticness","Instrumental","Liveness"),
                                       choiceNames=c("Danceability","Energy","Tempo","Duration",
                                                     "Loudness","Speechiness","Valence",
                                                     "Acousticness","Instrumental","Liveness")),
                          radioButtons("sep", "Separate by:",
                                       choiceValues = c("none","Genre","Sex","Mode"),
                                       choiceNames = c("None","Genre","Sex of Artist","Mode"))
                   ),
                   column(6,
                          radioButtons("yvar", "Y Variable:",
                                       choiceValues=c("Danceability","Energy","Tempo","Duration",
                                                      "Loudness","Speechiness","Valence",
                                                      "Acousticness","Instrumental","Liveness"),
                                       choiceNames=c("Danceability","Energy","Tempo","Duration",
                                                     "Loudness","Speechiness","Valence",
                                                     "Acousticness","Instrumental","Liveness"))
                   )
                 )
               ),
               mainPanel(
                 conditionalPanel("input.sep == 'none'", plotOutput("plot2")),
                 conditionalPanel("input.sep != 'none'", plotOutput("sepPlot"))
               )
             )
    ),
    tabPanel("Descriptive Statistics",
             titlePanel("Descriptive Statistics"),
             sidebarPanel(radioButtons("vars", "Variables:", choices = c("quantitative","genre","sex","mode"))),
             mainPanel(
               conditionalPanel("input.vars == 'quantitative'", dataTableOutput('summarytable')),
               conditionalPanel("input.vars == 'genre'", dataTableOutput('genretable')),
               conditionalPanel("input.vars == 'sex'", dataTableOutput('sexofartisttable')),
               conditionalPanel("input.vars == 'mode'", dataTableOutput('modetable'))
             )
    )
  )
)

server <- function(input, output, session) {
  output$plot <- renderPlot({
    dat <- subset(df, df$Genre %in% input$genre)
    titlestr<- paste("Song", input$x, "Across Genres")
    ggplot(data=dat,aes(x=get(input$x))) + 
      geom_density(aes(fill=(dat$Genre)),alpha=0.3) +
      labs(title=titlestr, x=input$x,y="Density",fill="Genre") +
      theme(axis.text.x=element_text(angle=65,hjust=1)) +
      theme_bw() + 
      scale_fill_brewer(palette = "Set1")
  })
  
  output$plot1 <- renderPlot({
    dat <- subset(df, df$Genre %in% input$genres)
    dat <- subset(dat, dat$Sex %in% input$sex)
    ggplot(dat, aes(artists)) +
      geom_bar(aes(fill = dat$Genre)) +
      
      ggtitle("Artist song counts by genre") +
      theme(axis.text.x=element_text(angle=65,hjust=1)) +
      labs(x = "Artist", y = "Count of Songs", fill = "Genre")+
      scale_fill_brewer(palette = "Set3")
  })
  
  
  output$plot2 <- renderPlot({
    mod <- lm(unlist(df[input$yvar]) ~ unlist(df[input$xvar]))
    pval <- unlist(summary(mod)$coefficients[,4][2])
    color <- ifelse(pval < 0.05, "green","#3995ce")
    mycaption <- paste(input$yvar, " = ", round(mod$coefficients[1],3), " + ",
                       round(mod$coefficients[2],3), "*", input$xvar, 
                       "\n Green regression lines have statistically significant slopes (alpha = 0.05)", sep="")
    ggplot(data = df, aes(x = get(input$xvar), y = get(input$yvar))) +
      geom_point(data = df, color = "#3995ce") +
      labs(x = input$xvar, y = input$yvar, caption=mycaption) +
      theme_bw() +
      geom_smooth(method = "lm", data = df, se = F, color = color) +
      ggtitle(paste(input$yvar, "vs", input$xvar))
  })
  
  output$sepPlot <- renderPlot({
    ggplot(data = df, aes(x = df[input$xvar], y = df[input$yvar])) +
      geom_point(data = df, color = "#3995ce") +
      facet_wrap(input$sep) +
      labs(x = input$xvar, y = input$yvar) +
      theme_bw() +
      geom_smooth(method = "lm", data = df, se = F, color = "#3995ce") +
      ggtitle(paste(input$yvar, "vs", input$xvar, "by", input$sep))
  })
  
  output$summarytable = DT::renderDataTable(({
    DT::datatable(quant_summary)
  }))
  
  output$genretable = DT::renderDataTable(({
    DT::datatable(genre_num)
  }))
  
  output$sexofartisttable = DT::renderDataTable(sex_num)
  
  output$modetable = DT::renderDataTable(({
    DT::datatable(mode_num)
  }))
}


shinyApp(ui, server)

