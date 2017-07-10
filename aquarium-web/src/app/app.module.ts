import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { ApiService } from './api.service';
import { CameraComponent } from './camera/camera.component';
import { LightComponent } from './light/light.component';
import { TemperatureComponent } from './temperature/temperature.component';
import { FanComponent } from './fan/fan.component';

@NgModule({
  declarations: [
    AppComponent,
    CameraComponent,
    LightComponent,
    TemperatureComponent,
    FanComponent
  ],
  imports: [
    BrowserModule,
    HttpModule,
    FormsModule
  ],
  providers: [
    ApiService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
