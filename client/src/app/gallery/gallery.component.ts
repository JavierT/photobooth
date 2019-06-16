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
  imgCount = 0;
  currentIndex = 0;

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

  getAll() {
    this.galleryService.getAll().subscribe(list => {
      console.log(list.gallery);
      this.gallery = list.gallery;
      this.imgCount = this.gallery.length;
      this.currentIndex = this.imgCount - 1;
      console.log('currentIndex,', this.currentIndex)
      this.mainImg = this.gallery[this.currentIndex];
      console.log('mainimg,', this.mainImg)
    });
  }

  initialize() {
    this.getAll();
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
        console.log('ws message ', message.action);
        switch (message.action) {
          case Actions.NEW:
            console.log('action new');
            this.getAll();
            break;
          case Actions.BACK:
            console.log('action BACK');
            this.currentIndex--;
            if (this.currentIndex < 0) {
              this.currentIndex = this.imgCount - 1;
            }
            this.mainImg = this.gallery[this.currentIndex];
            break;
          case Actions.NEXT:
            this.currentIndex++;
            if (this.currentIndex >= (this.imgCount)) {
              this.currentIndex = 0;
            }
            this.mainImg = this.gallery[this.currentIndex];
            console.log('action NEXT');
            break;
          default:
            break;
        }
      }
    );
  }

  getMainImgSrc() {
    console.log('get src', this.mainImg)
    if (this.mainImg) {
      console.log('http://localhost:5002/data/collages/' + this.mainImg.file)
      return 'http://localhost:5002/data/collages/' + this.mainImg.file;
    } else {
      return '';
    }

  }

  getThumbnailImgSrc(imgInfo: Thumbnail) {
    console.log('get src', imgInfo)
    if (imgInfo) {
      console.log('http://localhost:5002/data/thumbnails/' + imgInfo.file)
      return 'http://localhost:5002/data/thumbnails/' + imgInfo.file;
    } else {
      return '';
    }

  }

}
