import { addMilliseconds, differenceInCalendarDays, differenceInMilliseconds, format, formatDistanceToNowStrict, formatDistanceToNow, formatRelative, subDays, formatDistance, getHours, getSeconds, getMinutes } from "date-fns";



function convertTime(date: string, date_type: string = 'ago') {
    var timestamp = new Date();
    const posted_date = new Date(date); 
    const days = differenceInCalendarDays(timestamp, posted_date);
    const miliseconds = differenceInMilliseconds(posted_date, timestamp);


    
    if(date_type === 'ago') {
        // return formatDistance(new Date(), posted_date, { addSuffix: true, includeSeconds: true  })
        console.log(days)
        if(Math.abs(days) < 7) {
            return formatDistanceToNow(posted_date, { addSuffix: true, includeSeconds: true  })
        }
        // const date = format(posted_date, 'MMM dd, yyyy');
        // return date;
        const date = format(posted_date, 'MMM dd, yyyy - hh:mm a');
        const splt = date.split(' - ');
        return splt[0] + ' at ' + splt[1];
    }

    if(date_type === 'short' ) {
        if(Math.abs(days)  <= 0) {
            if(getHours(posted_date)) {
                return `${getHours(posted_date)}h`
            }
            else if(getMinutes(posted_date)) {
                return `${getMinutes(posted_date)}m`
            }
            else if(getSeconds(posted_date)) {
                return `${getSeconds(posted_date)}s`
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