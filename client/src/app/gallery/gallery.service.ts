import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class GalleryService {
  private url: string;

  constructor(private http: HttpClient) { 
    this.url = 'http://localhost:5002/api/';
  }

  getOne(imgName): Observable<any> {
    return this.http.get(this.url + 'gallery/'+ imgName).pipe(
      map(
        res => {
          return res;
        },
        err => {
          console.error('Service Image système', 'Echec requete get Liste tranches', err.message);
          return err;
        }
      )
    );
  }

  getAll(): Observable<any>  {
    return this.http.get(this.url + 'gallery').pipe(
      map(
        (res) => {
            return res;
          }
        )
    );
  }

}
