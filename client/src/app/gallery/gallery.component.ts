import { Component, OnInit, OnDestroy } from '@angular/core';
import { GalleryService } from './gallery.service';
import { switchMap, mergeMap } from 'rxjs/operators';
import { Observable, Subscription } from 'rxjs';
import { Thumbnail } from './thumbnail';

enum Actions {
  NONE = 0,
  NEW,
  BACK,
  NEXT
}

@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.scss']
})
export class GalleryComponent implements OnInit, OnDestroy {
  serverData: any;
  gallery: Thumbnail[];
  mainImg: any;
  public wsActionsSubscription: Subscription;

  constructor(private galleryService: GalleryService) {
   }

  ngOnInit() {
    this.mainImg = null;
    this.initialize();
  }

  ngOnDestroy() {
    this.galleryService.close();
    if (this.wsActionsSubscription) {
      this.wsActionsSubscription.unsubscribe();
    }
  }

  initialize() {
    this.galleryService.getAll().subscribe(list => {
        console.log(list);
      });
    // this.galleryService.getAll().pipe(
    //     mergeMap((listimgs) => {
    //       this.gallery = listimgs.gallery;
    //       console.log(this.gallery);
    //       if (this.gallery.length > 0) {
    //         //return this.galleryService.getOne(this.gallery[0].file);
    //         this.mainImg = 'http://localhost/collage/' + this.gallery[0].file
    //       }
    //     }
    //     )
    // ).subscribe(img => {
    //   console.log('main image:', img);
    //   this.mainImg = img; 
    // });

    this.wsActionsSubscription = this.galleryService.connect()
      .subscribe(message => {
        console.log('ws message ', message);
        switch (message.s_action) {
          case Actions.NEW:
            console.log('action new');
            break;
          default:
            break;
        }
      }
    );
  }

  getImgSrc(imgInfo: Thumbnail) {
    console.log('get src', imgInfo)
    if (imgInfo) {
      console.log('http://localhost/thumbnails/' + imgInfo.file)
      return 'http://localhost/thumbnails/' + imgInfo.file;
    } else {
      return '';
    }

  }

}
