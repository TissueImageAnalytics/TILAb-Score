# load packages required for the code in file

library(survival) 
library(survMisc)
library(gdata)
library(ggplot2)
library(survminer)
library(rms)

###########################################################################################
#                                 Utility Functions                                       #
###########################################################################################

best_threshold <- function(feature, time, event, no_quantiles = 13) {
  
  testrange=seq(0.01, 0.99, len=no_quantiles)
  p <- sapply(testrange, function(q){
    dat <- data.frame(x=feature>quantile(feature, q, na.rm=T),S=Surv(time,event))
    fit <- survfit(Surv(time,event) ~ x, data=dat)
    test <- survdiff(Surv(time,event) ~ x, data=dat, rho=0)
    p.val <- 1 - pchisq(test$chisq, length(test$n) - 1)
    p.val})
  
  # get best threshold
  q <- testrange[which.min(p)]
  th <- quantile(feature, q, na.rm=T)

  return(th)
}

KM_curve <- function(feature, time, event, threshold, save_plot = FALSE, filename = "", legend_title = "", legend_string = "") {
  
  temp <- feature > threshold
  temp <- as.numeric(temp)
  
  surv_data = data.frame(feature,time,event,temp)
  
  S <- Surv(time,event)
  test <- survdiff(S ~ temp, data= surv_data)
  best_p_value <- pchisq(test$chisq, length(test$n)-1, lower.tail = FALSE)
  
  res.cox <- coxph(Surv(time,event) ~ temp, data = surv_data)
  x <- summary(res.cox)
  
  HR <-signif(x$coef[2], digits=2)#exp(beta)
  CIlower <- signif(x$conf.int[,"lower .95"], 2)
  CIupper <- signif(x$conf.int[,"upper .95"], 2)
  LogLikely <- signif(x$logtest['pvalue'],3)
  LogRank <- signif(x$sctest['pvalue'],3)
  Wald <-signif(x$wald['pvalue'],3)
  
  
  if(save_plot == TRUE){
    # survfit(Surv(time,event) ~ temp, data=surv_data)
    survp <- ggsurvplot(survfit(Surv(time,event) ~ temp, data=surv_data), data=as.data.frame(surv_data),
                        legend.labs = legend_string, pval = TRUE, conf.int = FALSE, legend.title = legend_title,
                        font.main=16,font.x = 16,font.y = 16,font.legend=16,font.tickslab=16,
                        # Add risk table
                        risk.table = FALSE,
                        tables.height = 0.25,
                        ggtheme = theme_bw())
    print(survp, newpage = FALSE)
    dev.copy(png,filename)
    dev.off()
  }
  stats <- c(threshold, HR, CIlower, CIupper, LogLikely, LogRank, Wald)
  names(stats) <- c("Threshold","HR","CI(95%)-low","CI(95%)-high","LogLikely-pvalue","LogRank-pvalue","Wald-pvalue")
  return(stats)
}

# This function take one feature along with survival even and time data for both train and valid splits
# Output of this function is the KM curve and other survival statistics e.g. HR, CI, and pvalues etc.
Uni_Variate_Analysis <- function(train, valid, save_plot = FALSE, output_dir="", feature_name = "", legend_title = "", legend_string = "") {
  
  thr <- best_threshold(feature = train[,3], time = train[,2], event = train[,1])
  
  filename=sprintf("%s/%s_train.png", output_dir, feature_name)
  train_stats <- KM_curve(feature = train[,3], time = train[,2], event = train[,1], thr, save_plot = save_plot, filename = filename, legend_title = legend_title, legend_string = legend_string)
  print("Train Stats")
  print(train_stats)
  
  filename=sprintf("%s/%s_valid.png", output_dir, feature_name)
  valid_stats <- KM_curve(feature = valid[,3], time = valid[,2], event = valid[,1], thr, save_plot = save_plot, filename = filename, legend_title = legend_title, legend_string = legend_string)
  print("Test Stats")
  print(train_stats)
}