import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import * as Highcharts from 'highcharts';
import { DataService } from './services/data.service';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  @ViewChild('firstDialog') firstDialog: TemplateRef<any>;
  title = 'snafront';
  chartOptions: any = {};
  chartOptions2: any = {};
  updateFlag:boolean = false;
  updateFlag2:boolean = false;
  name: string;
  categories: string[];
  filteredItems: string[];
  selected: string;
  userId: number[];
  selectedId: number;
  Highcharts = Highcharts;
  show: boolean = false;
  movies_1: string ='';
  time_1:number = null;
  time_2:number = null;
  movies_2: string ='';
  selectedSplitList: number[] = [1, 2, 3];
  selectedSplit: number = this.selectedSplitList[0];
  graph:boolean = false;

  constructor(private data: DataService,  private dialog: MatDialog) { }


  ngOnInit() {
    this.data.getMovies().subscribe(res => {
      this.categories = res;
      this.filteredItems = this.categories;
      this.selected = this.categories[0];
    })

    this.data.getUserId().subscribe(res => {
      this.userId = res.sort((a,b)=> a-b);
      this.selectedId = this.userId[0];
    })

    this.chartOptions = {   
      chart: {
         type: 'column'
      },
      title: {
         text: 'Metrics for Recommendation'
      },
      subtitle:{
         text: 'SNA' 
      },
      xAxis:{
         categories: ['Accurancy','Recall','F1 Score','Precision'],
         crosshair: true        
      },     
      yAxis : {
         min: 0,
         title: {
            text: 'Y-Axis'         
         }      
      },
      plotOptions : {
         column: {
            pointPadding: 0.2,
            borderWidth: 0
         }
      },
      series: [{
         name: 'EnergySpreading',
         data: []
      }, 
      {
         name: 'UnionColors',
         data: []
      }]
   };
   this.chartOptions2 = {   
    chart: {
       type: 'column'
    },
    title: {
       text: 'Metrics for Recommendation'
    },
    subtitle:{
       text: 'SNA' 
    },
    xAxis:{
       categories: ['RMS','RMSE'],
       crosshair: true        
    },     
    yAxis : {
       min: 0,
       title: {
          text: 'Y-Axis'         
       }      
    },
    plotOptions : {
       column: {
          pointPadding: 0.2,
          borderWidth: 0
       }
    },
    series: [{
       name: 'EnergySpreading',
       data: []
    }, 
    {
       name: 'UnionColors',
       data: []
    }]
 };
   setTimeout(() => {
    this.updateFlag = true;
    window.dispatchEvent(new Event('resize'))
  }, 100);
  }


filterItem(value){

  this.filteredItems = Object.assign([], this.categories).filter(
     item => item.toLowerCase().indexOf(value.toLowerCase()) > -1
  )
  if(this.filteredItems.length) {
    this.selected = this.filteredItems[0];
  }
  else {
    this.selected = this.filteredItems[0];
  }
}

visualize_1() {
  this.data.getDataAlgo1(this.selected, this.selectedId, this.selectedSplit).subscribe(res => {
    if(res.error == 'error') {
      console.log('error...');
      this.openOtherDialog();
    }
    else {
      this.time_1 = res.time;
      this.chartOptions.series[0].data = [res.accuracy, res.recall,res.f1_score, res.precision];
      this.chartOptions2.series[0].data = [res.rms, res.rmsa];
      res.movies.forEach(element => {
        this.movies_1+=element + ', '
      });
      this.show=true;
      setTimeout(() => {
        this.updateFlag = true;
        this.updateFlag2 = true;
        window.dispatchEvent(new Event('resize'))
      }, 100);
    }
  });

}

visualize_2() {
  this.data.getDataAlgo2(this.selected, this.selectedId, this.selectedSplit).subscribe(res => {
    if(res.error == 'error') {
      console.log('error...');
      this.openOtherDialog();
    }
    else {
      console.log(res)
      this.time_2 = res.time;
      this.chartOptions.series[1].data = [res.accuracy, res.recall,res.f1_score, res.precision]
      this.chartOptions2.series[1].data = [res.rms, res.rmsa];
      this.show=true;
      res.movies.forEach(element => {
        this.movies_2+=element + ', '
      });
      setTimeout(() => {
        this.updateFlag = true;
        this.updateFlag2 = true;
        window.dispatchEvent(new Event('resize'))
      }, 100);
    }

  })

}

clearData() {
  this.graph = false;
  this.chartOptions.series[0].data = [];
  this.chartOptions.series[1].data = [];
  this.chartOptions2.series[0].data = [];
  this.chartOptions2.series[1].data = [];
  this.movies_1 ='';
  this.movies_2 ='';
  this.time_1 = null;
  this.time_2 = null;
  this.show = false;
  setTimeout(() => {
    this.updateFlag = true;
    this.updateFlag2 = true;
    window.dispatchEvent(new Event('resize'))
  }, 100);
}

openOtherDialog() {
  this.dialog.open(this.firstDialog);
}

showPlot() {
  this.graph = !this.graph;
}

}
