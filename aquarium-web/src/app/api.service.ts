import { Injectable } from '@angular/core';
import { Http, Response, RequestOptions, Headers } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

@Injectable()
export class ApiService {

  private baseUrl = 'http://gerty:8080/api';

  private registeredComponent;

  constructor(private http: Http) { }

  register(component) {
    this.registeredComponent = component;
    this.updateState();
  }

  updateState() {
    this.getState().subscribe(state => this.registeredComponent.state = state);
  }

  getState(): Observable<any> {
    const state$ = this.http
      .get(`${this.baseUrl}/controller/aqua`)
      .map(this.toJSON);
    return state$;
  }

  sendValues(values) {
    const state = {
      'controllerId': 'aqua',
      'values': values
    };
    const headers = new Headers({ 'Content-Type': 'application/json' });
    const options = new RequestOptions({ headers: headers });
    this.http
      .post(`${this.baseUrl}/updateController`, JSON.stringify(state), options)
      .toPromise()
      .then(() => this.updateState());
  }

  toJSON(response: Response): any {
    const json = response.json();
    console.log(json);
    return json;
  }
}
