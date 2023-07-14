type IntersectionCallback = (entry: IntersectionObserverEntry) => void;
type NotIntersectingCallback = (entry: IntersectionObserverEntry) => void;

// Create a reusable Intersection Observer function
function createIntersectionObserver(
  target: Element,
  callback: IntersectionCallback,
  options?: IntersectionObserverInit,
  observeOnce: boolean = true
): IntersectionObserver {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
          if(observeOnce){
            callback(entry);
            observer.disconnect()
          }
          else{
            callback(entry);
          }
        }
        else{
          if(!observeOnce) {
            callback(entry);
          }
        }
    });
  }, options);

  observer.observe(target);

  return observer;
}

export default createIntersectionObserver;