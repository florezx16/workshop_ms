from django.shortcuts import render
from django.views.generic import TemplateView
from .utils import pieChart_widgetData, barChart_widgetData, getLastInventoryMovements

# Create your views here.
class index_TemplateView(TemplateView):
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        barChartData = barChart_widgetData()
        monthNames = barChartData.get('monthsInfo')
        context["active_link"] = 'index'
        context["pieChartData"] = pieChart_widgetData()
        context["barChart_totalCompleted"] = barChartData.get('totalCompleted')
        context["barChart_totalCanceled"] = barChartData.get('totalCanceled')
        context["barChart_monthName1"] = monthNames.get('month1')
        context["barChart_monthName2"] = monthNames.get('month2')
        context["barChart_monthName3"] = monthNames.get('month3')
        context["inventoryMovements_query"] = getLastInventoryMovements()
        return context
    



    
