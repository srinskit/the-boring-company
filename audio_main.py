from custom_tunnel import NWInterface
from audio_tunnel import Tunnel
import argparse


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-p',
		'--peer',
		choices=['yin', 'yang'],
		required=True,
		help='The peer name'
	)
	parser.add_argument(
		'-r',
		'--relay-url',
		required=True,
		help='The relay url'
	)
	args = parser.parse_args()
	ip, port = args.relay_url.split(':')
	tunnel = Tunnel(args.peer, (ip, int(port)))

	intf = NWInterface(tunnel, name='%s-tun' % args.peer)

	intf.tun.addr = '10.0.0.1' if args.peer == 'yin' else '10.0.0.2'
	intf.tun.dstaddr = '10.0.0.2' if args.peer == 'yin' else '10.0.0.1'
	intf.tun.netmask = '255.255.255.0'
	intf.tun.mtu = 128

	intf.up()
	try:
		input('Enter to quit')
	except KeyboardInterrupt:
		pass

	intf.down()


if __name__ == '__main__':
	main()
