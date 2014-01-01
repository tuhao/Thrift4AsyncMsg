package main

import (
	"crawler"
	"flag"
	"fmt"
	"git.apache.org/thrift.git/lib/go/thrift"
	"os"
)

func runServer(transportFactory thrift.TTransportFactory, protocolFactory thrift.TProtocolFactory, addr string) error {
	transport, err = thrift.NewTServerSocket(addr) //simple case
	if err != nil {
		return err
	}
	handler := &dataServiceProcessorPull{}
	processor := crawler.NewDataServiceProcessor(handler)
	server := thrift.NewTSimpleServer(processor, transport, transportFactory, protocolFactory)
	fmt.Println("Starting the simple server... on ", transport.Addr())
	server.serve()
}

func Usage() {
	fmt.Fprint(os.Stderr, "Usage of ", os.Args[0], ":\n")
	flag.PrintDefaults()
	fmt.Fprint(os.Stderr, "\n")
}

func main() {
	flag.Usage = Usage
	protocol := flag.String("P", "binary", "Specify the protocol (binary,compact,simplejson)")
	framed := flag.Bool("framed", true, "Use framed transport")
	bufferd := flag.Bool("bufferd", true, "Use bufferd transport")
	addr := flag.String("addr", "localhost:9090", "Address to listen to")
	flag.Parse()

	var protocolFactory thrift.TProtocolFactory
	switch *protocol {
	case "compact":
		protocolFactory = thrift.NewTCompactProtocolFactory()
	case "simplejson":
		protocolFactory = thrift.NewTSimpleJSONProtocolFactory()
	case "json":
		protocolFactory = thrift.NewTJSONProtocolFactory()
	case "binary", "":
		protocolFactory = thrift.NewTBinaryProtocolFactoryDefault()
	default:
		fmt.Fprint(os.Stderr, "Invalid protocol specified", protocol, "\n")
		Usage()
		os.Exit(1)
	}

	var transportFactory thrift.TTransportFactory
	if *bufferd {
		transportFactory = thrift.NewTBufferedTransportFactory(8192)
	} else {
		transportFactory = thrift.NewTTranspotFactory()
	}
	if *framed {
		transportFactory = thrift.NewTFramedTranspotFactory(transportFactory)
	}
	if err := runServer(transportFactory, protocolFactory, addr); err != nil {
		fmt.Println("error running server:", err)
	}
}
