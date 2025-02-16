import type { PageLoad } from './$types';

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const load: PageLoad = async ({ params }) => {
	console.log({ params });
	await sleep(3000);
	return {
		id: '121212',
		name: 'Google',
		url: 'http://google.com',
		status: 'SUCCESS',
		paused: false,
		beats: [
			{ id: '1', date: '2025-02-15T10:27:01Z', status_code: 400 },
			{
				id: '2',
				date: '2025-02-15T10:28:01Z',
				status_code: 200
			},
			{
				id: '3',
				date: '2025-02-15T10:29:01Z',
				status_code: 200
			}
		],
		frequency: '5 Minutes'
	};
};
