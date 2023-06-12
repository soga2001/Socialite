export function getParentRouterPath(instance: any) {
    try {
        console.log(instance)
        return instance.$parent.$route.meta.basePath;
    } catch (e) {
        return "";
    }
  }