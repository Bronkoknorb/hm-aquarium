import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-fan',
  templateUrl: './fan.component.html',
  styleUrls: ['./fan.component.scss']
})
export class FanComponent implements OnInit {

  @Input() on;

  constructor() { }

  ngOnInit() {
  }

}
