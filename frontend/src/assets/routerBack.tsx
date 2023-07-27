import {useRoute} from 'vue-router'
import router from '@/router';

export default function useRouteBack() {

    const route = useRoute();

    if(route.path === '/') {
      router.push('/explore')
    }
    else {
      router.back()
    }
}

