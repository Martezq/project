class WorkoutTimer {
    constructor(workout) {
        this.workout = workout;
        this.currentIntervalIndex = -1;
        this.intervalId = null;
        this.isRecovery = false;
        this.isOvertime = false;
        this.readyButton = document.getElementById('readyButton');
        this.stopButton = document.getElementById('stopButton');
        this.currentIntervalTimeLeft = 0; 
        this.currentIntervalTimer = null; 
        this.currentIntervalDisplay = document.getElementById('currentIntervalTimer');
        this.nextIntervalDisplay = document.getElementById('nextInterval');
        this.totalDurationTimer = null; 
        this.workoutStartTime = null; 

    }

    start() {
        this.workoutStartTime = Date.now();
        this.stopButton.disabled = false;
        this.totalDurationTimer = setInterval(() => {
            let duration = Date.now() - this.workoutStartTime;
            let minutes = Math.floor(duration / 60000);
            let seconds = ((duration % 60000) / 1000).toFixed(0);
            document.getElementById('totalTimeTaken').innerText = minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
        }, 1000);
        this.nextInterval();
    }

    ready() {
        if (this.isRecovery || this.isOvertime) {
            this.isRecovery = false;
            console.log('Ready button pressed. Waiting for the remaining recovery period before starting high-intensity.');
    
            if (this.intervalId !== null) {
                clearInterval(this.intervalId);
            }
    
            if (!this.isOvertime) {
                let remainingTime = (this.endTime - Date.now());
                this.intervalId = setTimeout(() => {
                    this.nextInterval();
                }, remainingTime);
            } else {
                this.isOvertime = false;
                this.overtimeStartTime = null;
                this.intervalId = setTimeout(() => {
                    this.nextInterval();
                }, 10 * 1000);
                console.log('Ready button pressed. Starting high-intensity in 10 seconds.');
            }   this.currentIntervalTimeLeft = 10;
                this.currentIntervalDisplay.innerText = this.formatTime(this.currentIntervalTimeLeft);
        }
    }
    
    nextInterval() {
        this.currentIntervalIndex++;
        if (this.currentIntervalIndex >= this.workout.intervals.length) {
            this.stop();
            this.nextIntervalDisplay.innerText = 'End of workout';
            return;
        }
    
        const interval = this.workout.intervals[this.currentIntervalIndex];

        if (this.currentIntervalIndex + 1 < this.workout.intervals.length) {
            this.nextIntervalDisplay.innerText = this.workout.intervals[this.currentIntervalIndex + 1].type;
        } else {
            this.nextIntervalDisplay.innerText = 'End of workout';
        }

        if (this.currentIntervalIndex === this.workout.intervals.length - 1 && interval.type === 'recovery') {
            this.stop();
            return;
        }


        this.isRecovery = interval.type === 'recovery';
        this.readyButton.disabled = !this.isRecovery;

        this.currentIntervalTimeLeft = interval.duration;
        this.currentIntervalDisplay.innerText = this.formatTime(this.currentIntervalTimeLeft);

        if (this.currentIntervalTimer !== null) {
            clearInterval(this.currentIntervalTimer);
        }

        this.currentIntervalTimer = setInterval(() => {
            this.currentIntervalTimeLeft -= 1;
            this.currentIntervalDisplay.innerText = this.formatTime(this.currentIntervalTimeLeft);
            if (this.currentIntervalTimeLeft <= 0) {
                clearInterval(this.currentIntervalTimer);
                this.currentIntervalTimer = null;
            }
        }, 1000);

        if (this.isRecovery) {
            this.endTime = Date.now() + interval.duration * 1000;
            this.recoveryDuration = interval.duration;
            this.intervalId = setInterval(() => {
                let remainingTime = (this.endTime - Date.now()) / 1000;
                if (remainingTime <= 0) {
                    if (!this.isOvertime) {
                        clearInterval(this.intervalId);
                        this.isOvertime = true;
                        this.overtimeStartTime = Date.now()
                        console.log("Overtime started.");
                    }
                }
            }, 1000);
        } else {
            this.intervalId = setTimeout(() => {
                this.nextInterval();
            }, interval.duration * 1000);
        }
        // Update interval timer every second
        if (this.currentIntervalTimer !== null) {
            clearInterval(this.currentIntervalTimer);
        }
        this.currentIntervalTimer = setInterval(() => {
            if (!this.isOvertime) {
                this.currentIntervalTimeLeft -= 1;
                if (this.currentIntervalTimeLeft <= 0) {
                    clearInterval(this.currentIntervalTimer);
                    this.currentIntervalTimer = null;
                }
            } else {
                // In overtime, we count up from zero
                this.currentIntervalTimeLeft = Math.floor((Date.now() - this.overtimeStartTime) / 1000);
            }
            this.currentIntervalDisplay.innerText = this.formatTime(this.currentIntervalTimeLeft);
        }, 1000);
        // This is where you would update your UI
        console.log(`Starting ${interval.type} for ${interval.duration} seconds`);
    }
    
    
    formatTime(seconds) {
        let minutes = Math.floor(seconds / 60);
        seconds = seconds % 60;
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }
    

    stop() {
        if (this.intervalId !== null) {
            clearTimeout(this.intervalId);
            this.intervalId = null;
        }

        if (this.currentIntervalTimer !== null) {
            clearInterval(this.currentIntervalTimer);
            this.currentIntervalTimer = null;
        }
        if (this.totalDurationTimer !== null) {
            clearInterval(this.totalDurationTimer);
            this.totalDurationTimer = null;
        }
        this.isOvertime = false;
        this.overtimeStartTime = null;
        this.isRecovery = false;
        this.stopButton.disabled = true; 
        this.readyButton.disabled = true;
        this.nextIntervalDisplay.innerText ='Warm-up'; 
        console.log("Workout ended");
    }    
}



document.addEventListener('DOMContentLoaded', (event) => {
    const startButton = document.getElementById('startButton');
    const readyButton = document.getElementById('readyButton');
    const stopButton = document.getElementById('stopButton');
    const currentIntervalTimer = document.getElementById('currentIntervalTimer');
    const totalTimeLeft = document.getElementById('totalTimeLeft');
    const nextInterval = document.getElementById('nextInterval');
    const workoutTimer = document.querySelector('.workout-timer');

    let warmUpDuration = parseInt(workoutTimer.dataset.warmup);
    let highIntensityDuration = parseInt(workoutTimer.dataset.highintensity);
    let recoveryDuration = parseInt(workoutTimer.dataset.recovery);
    let numberOfIntervals = parseInt(workoutTimer.dataset.intervals);

    let timer = null; // Define the timer variable in the scope accessible to both event listeners.

    startButton.addEventListener('click', function() {
        const workoutData = {
            intervals: [
                {type: 'warm-up', duration: warmUpDuration},
                {type: 'high-intensity', duration: highIntensityDuration},
                {type: 'recovery', duration: recoveryDuration},
                // repeat high-intensity and recovery for the number of intervals
                ...Array(numberOfIntervals).fill().flatMap(() => [
                    {type: 'high-intensity', duration: highIntensityDuration},
                    {type: 'recovery', duration: recoveryDuration},
                ]),
            ]
        };
    
        timer = new WorkoutTimer(workoutData);
        timer.start();
    });
    

    readyButton.addEventListener('click', function() {
        if (timer) timer.ready();
    });

    stopButton.addEventListener('click', function() {
        if (timer) timer.stop();
    });
});

