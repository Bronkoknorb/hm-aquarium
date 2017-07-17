import { Component, OnInit } from '@angular/core';

import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';

import { ApiService } from '../api.service';

@Component({
  selector: 'app-top-off',
  templateUrl: './top-off.component.html',
  styleUrls: ['./top-off.component.scss']
})
export class TopOffComponent {

  closeResult: string;

  duration: number;

  constructor(private modalService: NgbModal, private api: ApiService) {}

  open(content) {
    this.modalService.open(content).result.then((result) => {
      this.api.sendValues({
        'top_off_duration': this.duration
      });
      this.duration = null;
    });
  }

  isValid() {
    return this.duration;
  }

}
