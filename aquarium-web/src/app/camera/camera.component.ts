import { Component, OnInit, Input, ElementRef, ViewChild } from '@angular/core';
import {  } from '@angular/core';

@Component({
  selector: 'app-camera',
  templateUrl: './camera.component.html',
  styleUrls: ['./camera.component.scss']
})
export class CameraComponent implements OnInit {

  @Input() websocketAddress: string;

  @ViewChild('img') img: ElementRef;

  fullscreen = false;

  webSocket: WebSocket = null;

  constructor() { }

  ngOnInit() {
    document.addEventListener('visibilitychange', () => this.handleVisibilityChange(), false);
    this.handleVisibilityChange();
  }

  handleVisibilityChange() {
    if (document['hidden']) {
      console.log('Stopping Video ' + this.websocketAddress);
      this.stopVideo();
    } else {
      console.log('Starting Video ' + this.websocketAddress);
      this.startVideo();
    }
  }

  toggleFullscreen() {
    const fullscreenElement = document.fullscreenElement || (<any>document).mozFullScreenElement || document.webkitFullscreenElement;
    const fullscreenEnabled = fullscreenElement != null;

    function launchIntoFullscreen(element) {
      if (element.requestFullscreen) {
        element.requestFullscreen();
      } else if (element.mozRequestFullScreen) {
        element.mozRequestFullScreen();
      } else if (element.webkitRequestFullscreen) {
        element.webkitRequestFullscreen();
      } else if (element.msRequestFullscreen) {
        element.msRequestFullscreen();
      }
    }

    function exitFullscreen() {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if ((<any>document).mozCancelFullScreen) {
        (<any>document).mozCancelFullScreen();
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
      }
    }

    if (fullscreenEnabled) {
      this.fullscreen = false;
      exitFullscreen();
    } else {
      this.fullscreen = true;
      launchIntoFullscreen(this.img.nativeElement);
    }
  }

  startVideo() {
    if (this.webSocket !== null) {
      return; // video already started
    }

    const target_fps = 24;
    const img = this.img;

    let request_start_time = performance.now();
    let start_time = performance.now();
    let time = 0;
    let request_time = 0;
    const time_smoothing = 0.9; // larger=more smoothing
    const request_time_smoothing = 0.2; // larger=more smoothing
    const target_time = 1000 / target_fps;

    this.webSocket = new WebSocket(this.websocketAddress);
    this.webSocket.binaryType = 'arraybuffer';

    const requestImage = () => {
      request_start_time = performance.now();
      if (this.webSocket !== null) {
        this.webSocket.send('more');
      }
    }

    this.webSocket.onopen = () => {
      start_time = performance.now();
      requestImage();
    };

    this.webSocket.onmessage = (evt) => {
      const arrayBuffer = evt.data;
      const blob = new Blob([new Uint8Array(arrayBuffer)], { type: 'image/jpeg' });
      img.nativeElement.src = window.URL.createObjectURL(blob);

      const end_time = performance.now();
      const current_time = end_time - start_time;
      // smooth with moving average
      time = (time * time_smoothing) + (current_time * (1.0 - time_smoothing));
      start_time = end_time;

      const current_request_time = performance.now() - request_start_time;
      // smooth with moving average
      request_time = (request_time * request_time_smoothing) + (current_request_time * (1.0 - request_time_smoothing));
      const timeout = Math.max(0, target_time - request_time);

      setTimeout(requestImage, timeout);
    };
  }

  stopVideo() {
    if (this.webSocket === null) {
      return; // video already stopped
    }

    this.webSocket.close();
    this.webSocket = null;
  }
}
