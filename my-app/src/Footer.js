import React, { Component } from 'react';
import UserConfirmationModal from './UserConfirmationModal';
import './Footer.css';
import Calendar from './Calendar';
import MonthCalendar from './MonthCalendar';
import YearCalendar from './YearCalendar';
import MapChart from './MapChart';
import './MapChart.css';

 
class Footer extends Component {
	
    constructor(props) {
        super(props);
        this.state = {
            modalVisible: false
        };
        
        this.showModal = this.showModal.bind(this);
        this.hideModal = this.hideModal.bind(this);
		this.handleChange = this.handleChange.bind(this);
    }
	
	handleChange(event) {
    this.setState({value: event.target.value});
  }
    
    showModal() {
        console.log('show modal');
        this.setState({modalVisible:true});
    }
    
    hideModal(userChoice) {
        //handle user choice
        console.log(userChoice);
        this.setState({modalVisible:false});
    }
            
    render() { 
        return (            
            <div className="row">
				<div class="column left">
					<h2><u>Choose your data set</u></h2> 
					<br />
					<div class="data-set">
					<h4>Choose economic zone:</h4>
					<br />
					<div class="dropdown-content">
					<select value={this.state.value} onChange={this.handleChange}>
						<option value="FR">France</option>
						<option value="GER">Germany</option>
						<option value="GR">Greece</option>
						<option value="UK">United Kingdom</option>
					</select>
					</div>
					<br />
					</div>
					<br />
					<div class="data-set">
					<h4>Please select <strong>only</strong> one below:</h4>
					<br />
					<p>Choose day:</p>
					<Calendar />	
					<br />
					<p>Choose month:</p>
					<MonthCalendar />	
					<br />
					<p>Choose year:</p>
					<div class="center">
					<YearCalendar />
					</div>
					<br />
					</div>
					<br />
					<div class="data-set">
					<h4>Choose data type:</h4>
					<br />
					<input type="radio" id="dia" name="datatype" value="diagramm"/>
					<label> Diagramm &nbsp; &nbsp; &nbsp; &nbsp;</label>
					<input type="radio" id="js" name="datatype" value="json"/>
					<label>Json</label>
					</div>
					<br />
					<button className="btn btn-info" onClick={this.showModal}>Confirm</button>
                    <UserConfirmationModal 
                        title="Confirm something"
                        message="Are you sure?"
                        visible={this.state.modalVisible} 
                        onHide={this.hideModal}
                    />
				</div>
					<div class="column right">
					<br /> <br />
					<MapChart />
					</div>
				</div>
            
            
        );
    }
    
}

export default Footer;