import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { ApiService } from './api.service';
import { CameraComponent } from './camera/camera.component';
import { LightComponent } from './light/light.component';

@NgModule({
  declarations: [
    AppComponent,
    CameraComponent,
    LightComponent
  ],
  imports: [
    BrowserModule,
    HttpModule
  ],
  providers: [
    ApiService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
