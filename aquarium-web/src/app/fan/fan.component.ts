import { Component, OnInit, Input } from '@angular/core';

import { ApiService } from '../api.service';

@Component({
  selector: 'app-fan',
  templateUrl: './fan.component.html',
  styleUrls: ['./fan.component.scss']
})
export class FanComponent implements OnInit {

  on = false;
  turn_on_temperature: number;
  turn_off_temperature: number;

  constructor(private api: ApiService) { }

  ngOnInit() {
  }

  @Input() set state(state) {
    if (state == null) {
      return;
    }
    this.on = state.values.fan === 1;
    this.turn_on_temperature = state.values.fan_turn_on_temperature;
    this.turn_off_temperature = state.values.fan_turn_off_temperature;
  }

  save() {
    this.api.sendValues({
      'fan_turn_on_temperature': this.turn_on_temperature,
      'fan_turn_off_temperature': this.turn_off_temperature
    });
  }

}
