import { Component, OnInit, Input } from '@angular/core';

import { ApiService } from '../api.service';

@Component({
  selector: 'app-light',
  templateUrl: './light.component.html',
  styleUrls: ['./light.component.scss']
})
export class LightComponent {

  moonlight = false;
  sunlight = false;
  lightsoff = false;

  constructor(private api: ApiService) {
  }

  @Input() set state(state) {
    if (state == null) {
      return;
    }
    this.moonlight = state.values.moonlight === 1;
    this.sunlight = state.values.sunlight === 1;
    this.lightsoff = !this.moonlight && !this.sunlight;
  }

  turnSunlightOn() {
    const values = {
      'sunlight': 1
    };
    if (this.moonlight) {
      values['moonlight'] = 0;
    }
    this.send(values);
  }

  turnMoonlightOn() {
    const values = {
      'moonlight': 1
    };
    if (this.sunlight) {
      values['sunlight'] = 0;
    }
    this.send(values);
  }

  turnLightsOff() {
    const values = {
      'sunlight': 0,
      'moonlight': 0
    };
    this.send(values);
  }

  send(values) {
    this.api.sendValues(values);
  }
}
