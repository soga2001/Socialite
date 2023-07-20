import { addMilliseconds, differenceInCalendarDays, differenceInMilliseconds, format, formatDistanceToNowStrict, formatDistanceToNow, formatRelative, subDays } from "date-fns";



function convertTime(date: string, date_type: string = 'ago') {
    var timestamp = new Date();
    const posted_date = new Date(date); 
    const days = differenceInCalendarDays(timestamp, posted_date);
    const miliseconds = differenceInMilliseconds(posted_date, timestamp);


    console.log(date_type)
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

    if(date_type == 'absolute') {
        if(Math.abs(days) < 7) {
            const date = new Date();
            return formatRelative(addMilliseconds(date, miliseconds), date);
        }
        const date = format(posted_date, 'MMM dd, yyyy - hh:mm a');
        const splt = date.split(' - ');
        return splt[0] + ' at ' + splt[1];
    }
    else {
        const date = format(posted_date, 'MMM dd, yyyy');
        return date;
    }
}

export default convertTime;