type IntersectionCallback = (entry: IntersectionObserverEntry) => void;

// Create a reusable Intersection Observer function
function createIntersectionObserver(
  target: Element,
  callback: IntersectionCallback,
  options?: IntersectionObserverInit
): IntersectionObserver {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            // console.log(entry.intersectionRatio)
            // if (entry.intersectionRatio >= 0.75) {
                
            // }
            callback(entry);
            observer.disconnect()
        }
    });
  }, options);

  observer.observe(target);

  return observer;
}

export default createIntersectionObserver;