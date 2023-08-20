import { addMilliseconds, differenceInCalendarDays, differenceInHours, differenceInSeconds, differenceInMinutes, differenceInMilliseconds, format, formatDistanceToNowStrict, formatDistanceToNow, formatRelative, subDays, formatDistance, getHours, getSeconds, getMinutes } from "date-fns";



function convertTime(date: string, date_type: string = 'ago') {
    var timestamp = new Date();
    const posted_date = new Date(date); 
    const days = differenceInCalendarDays(timestamp, posted_date);
    const miliseconds = differenceInMilliseconds(posted_date, timestamp);


    
    if(date_type === 'ago') {
        if(Math.abs(days) < 7) {
            return formatDistanceToNow(posted_date, { addSuffix: true, includeSeconds: true  })
        }
        
        const date = format(posted_date, 'MMM dd, yyyy - hh:mm a');
        const splt = date.split(' - ');
        return splt[0] + ' at ' + splt[1];
    }

    if(date_type === 'short' ) {
        if(Math.abs(days)  <= 0) {
            // Calculate the difference in hours between the posted date and the current date
            const hoursDifference = differenceInHours(timestamp, posted_date);

            // Calculate the difference in seconds between the posted date and the current date
            const secondsDifference = differenceInSeconds(timestamp, posted_date);

            // Calculate the difference in minutes between the posted date and the current date
            const minutesDifference = differenceInMinutes(timestamp, posted_date);

            // If the difference in hours is greater than 0, return the difference in hours
            if(hoursDifference > 0 && hoursDifference !== 0) {
                return hoursDifference + 'h';
            }
            // Else if the difference in minutes is less or equal to 59 (less then an
            // hour), return the difference in minutes
            else if(minutesDifference <= 59 && minutesDifference !== 0) {
                return minutesDifference + 'm';
            }
            // Else if the difference in seconds is less or equal to 59 (less then a
            // minute), return the difference in seconds
            else if(secondsDifference <= 59) {
                return secondsDifference + 's';
            }
        }
        return format(posted_date, 'MMM dd')
    }

    if(date_type == 'absolute') {
        // if(Math.abs(days) < 7) {
        //     const date = new Date();
        //     return formatRelative(addMilliseconds(date, miliseconds), date);
        // }
        const date = format(posted_date, 'hh:mm a &#183 MMM dd, yyyy');
        return date
        // const splt = date.split(' - ');
        // return splt[0] + ' at ' + splt[1];
    }
    else {
        const date = format(posted_date, 'MMM dd, yyyy');
        return date;
    }
}

export default convertTime;