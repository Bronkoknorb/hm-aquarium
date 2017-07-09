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

  constructor() { }

  ngOnInit() {
    const target_fps = 24;
    const img = this.img;

    let request_start_time = performance.now();
    let start_time = performance.now();
    let time = 0;
    let request_time = 0;
    const time_smoothing = 0.9; // larger=more smoothing
    const request_time_smoothing = 0.2; // larger=more smoothing
    const target_time = 1000 / target_fps;

    const ws = new WebSocket(this.websocketAddress);
    ws.binaryType = 'arraybuffer';

    function requestImage() {
        request_start_time = performance.now();
        ws.send('more');
    }

    ws.onopen = function() {
        start_time = performance.now();
        requestImage();
    };

    ws.onmessage = function(evt) {
        const arrayBuffer = evt.data;
        const blob  = new Blob([new Uint8Array(arrayBuffer)], {type: 'image/jpeg'});
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

  toggleFullscreen() {
    this.fullscreen = !this.fullscreen;
  }

}
