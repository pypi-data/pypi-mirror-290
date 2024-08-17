


<script>

import Map from 'lucide-svelte/icons/map'
import Modal from './Modal.svelte'

import { getModalStore } from '@skeletonlabs/skeleton';
const modal_store = getModalStore ();
			

const open_map = () => {
	console.info ("open_map")
	
	modal_store.trigger ({
		type: 'component',
		component: {
			ref: Modal,
			props: { 
				modal_store
			}
		}
	});
}

</script>

<button on:click={ open_map } >
	<Map />
</button>