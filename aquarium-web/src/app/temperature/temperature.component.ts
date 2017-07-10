import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-temperature',
  templateUrl: './temperature.component.html',
  styleUrls: ['./temperature.component.scss']
})
export class TemperatureComponent implements OnInit {

  @Input() temp;

  @Input() label;

  constructor() { }

  ngOnInit() {
  }

}
