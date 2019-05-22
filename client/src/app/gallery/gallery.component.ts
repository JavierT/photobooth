import { Component, OnInit } from '@angular/core';
import { GalleryService } from './gallery.service';
import { switchMap, mergeMap } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { Thumbnail } from './thumbnail';


@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.scss']
})
export class GalleryComponent implements OnInit {
  serverData: any;
  gallery: Thumbnail[];
  mainImg: any;

  constructor(private galleryService: GalleryService) {
   }

  ngOnInit() {
    this.initialize();
  }

  initialize() {
    this.galleryService.getAll().pipe(
        mergeMap((listimgs) => {
          this.gallery = listimgs.gallery;
          console.log(this.gallery);
          if (this.gallery.length > 0) {
            return this.galleryService.getOne(this.gallery[0].file);
          }
        }
        )
    ).subscribe(img => {
      console.log('main image:', img);
      this.mainImg = img; });
  }

  getImgSrc(imgInfo: Thumbnail) {
    console.log('get src', imgInfo)
    if (imgInfo) {
      console.log('http://localhost:5002/api/' + imgInfo.file)
      return 'http://localhost:5002/api/' + imgInfo.file;
    } else {
      return '';
    }

  }

}
