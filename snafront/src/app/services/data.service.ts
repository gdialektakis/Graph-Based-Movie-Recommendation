import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { Data } from '../Models/Data';

const URL1 = 'http://160.40.53.168:5001/EnergySpreading';
const URL2 = 'http://160.40.53.168:5001/UnionColors';
const URL3 = 'http://160.40.53.168:5001/movies';
const URL4 = 'http://160.40.53.168:5001/userId';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json','Access-Control-Allow-Origin': '*' })
};


@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private http: HttpClient) {
  }

  getMovies(): Observable<string[]>{
    return this.http.get<string[]>(URL3, httpOptions);
  }

  getUserId(): Observable<number[]> {
    return this.http.get<number[]>(URL4, httpOptions);
  }

  getDataAlgo1(category: string,userId: number, ratio: number): Observable<Data> {
    let params = new HttpParams().set('category', category).set('userId',userId.toString()).set('ratio',ratio.toString())
    //return of({rmsa: 50, accurancy:50, f1_score: 50, precision:10, recall: 70, rms: 78})
    return this.http.get<Data>(URL1, {params: params, headers: httpOptions.headers});
  }

  getDataAlgo2(category: string, userId: number, ratio: number): Observable<Data> {
    let params = new HttpParams().set('category', category).set('userId',userId.toString()).set('ratio',ratio.toString())
    //return of({rmsa: 50, accurancy:50, f1_score: 50, precision:10, recall: 70, rms: 78})
    return this.http.get<Data>(URL2, {params: params, headers: httpOptions.headers});
  }


}
