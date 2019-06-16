import { Injectable } from '@angular/core';
import { retryWhen, share, map, delay } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { webSocket } from 'rxjs/webSocket';

@Injectable({
  providedIn: 'root'
})

export class GalleryService {
  private url: string;
  private ws_url: string;
  private host: string;
  private port: string;

  // WS
  readonly reload_time = 3000;
  public messages: Observable<any>;
  private ws: Subject<any>;
  public onclose = new Subject();

  constructor(private http: HttpClient) { 
    this.host = 'localhost';
    this.port = '5002';
    this.url = `http://${this.host}:${this.port}/api/`;
    this.ws_url = `ws://${this.host}:${this.port}/`;
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

  public connect(): Observable<any> {
    console.log('trying to connect to ws');
    this.ws = webSocket({
      url: this.ws_url + 'actions',
      closeObserver: this.onclose
    });
    return this.messages = this.ws.pipe(retryWhen(errors => errors.pipe(delay(this.reload_time))), map(msg => msg), share(), );
  }

  send(msg: any) {
    this.ws.next(JSON.stringify(msg));
  }

  public close() {
    this.ws.complete();
  }

}

