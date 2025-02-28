import { PUBLIC_BASE_URL } from '$env/static/public';
import type { PageLoad } from './$types';

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const load: PageLoad = async ({ params }) => {
	let url = `${PUBLIC_BASE_URL}/api/v1/event/${params.mid}/logs`;
	const r = await fetch(url);
	const events = await r.json();

	return {
		events
	};
};
