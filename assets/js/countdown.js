function updateBar(e){fillSecondBar(e[6]),fillMinuteBar(e[5]),fillHourBar(e[4]),fillDayBar(e[3]),fillTotalbar(e[6]+60*e[5]+60*e[4]*60+60*e[3]*60*24)}function fillSecondBar(e){$("#second-number").html(e),$("#second-bar").css("width",100*e/60+"%")}function fillMinuteBar(e){$("#minute-number").html(e),$("#minute-bar").css("width",100*e/60+"%")}function fillHourBar(e){$("#hour-number").html(e),$("#hour-bar").css("width",100*e/24+"%")}function fillDayBar(e){$("#day-number").html(e),$("#day-bar").css("width",100*e/365+"%")}function fillTotalbar(e){defaultPercent=100-100*e/difToSecond,currentPercent=defaultPercent>=10?defaultPercent.toString().substr(0,5):defaultPercent.toString().substr(0,4),$("#total-bar").css("width",defaultPercent+"%").html(currentPercent+"%")}var startDate=new Date("22/11/2014"),endDate=new Date("1/1/2016"),dif=endDate.getTime()-startDate.getTime(),difToSecond=dif/1e3,defaultPercent=0;$(function(){$("#counter").countdown({until:endDate,layout:"<div></div>",onTick:updateBar}),$("a[rel=tooltip]").tooltip(),$("div[rel=tooltip]").tooltip()});