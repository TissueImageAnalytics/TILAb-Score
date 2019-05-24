## remove (almost) everything in the working environment.
## You will get no warning, so don't do this unless you are really sure.
rm(list = ls()) 

# add utility functions to the path
source("survival_utils.r") 

output_dir <- "../results/"
legend_title = "TILAb Score:"
legend = c("High Risk", "Low Risk")

# loading survival data required for analysis
# CSV file should consist of three columns (Event, Time, TILAb_Score)
train <- read.csv(file="../survival_data/dummy_train.csv", header=TRUE, sep=",")
valid <- read.csv(file="../survival_data/dummy_valid.csv", header=TRUE, sep=",")

Uni_Variate_Analysis(train, valid, save_plot = FALSE, output_dir=output_dir, feature_name = "TILAb_Score", legend_title = legend_title, legend_string = legend)