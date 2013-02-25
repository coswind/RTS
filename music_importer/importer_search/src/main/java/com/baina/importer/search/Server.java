package com.baina.importer.search;

import java.util.Timer;

import org.apache.thrift.TProcessorFactory;
import org.apache.thrift.protocol.TCompactProtocol;
import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TThreadedSelectorServer;
import org.apache.thrift.transport.TFramedTransport;
import org.apache.thrift.transport.TNonblockingServerSocket;

import com.baina.importer.search.service.thrift.SearchService;

public class Server {
    public static void main(String[] args) {
        try {
            TNonblockingServerSocket socket = new TNonblockingServerSocket(9090);
            final SearchService.Processor<SearchServiceImpl> processor = new SearchService.Processor<SearchServiceImpl>(
                new SearchServiceImpl());
            TThreadedSelectorServer.Args arg = new TThreadedSelectorServer.Args(socket);
            arg.protocolFactory(new TCompactProtocol.Factory());
            arg.transportFactory(new TFramedTransport.Factory());
            arg.processorFactory(new TProcessorFactory(processor));

            TServer server = new TThreadedSelectorServer(arg);
            String msg = String.format("server %s is started, listening on port:%d", server
                                       .getClass().getName(), 9090);
            System.out.println(msg);
            
            Timer timer = new Timer("MySearchTimer", true);
            timer.schedule(new MySearchTask(), 0, 1 * 60 * 1000);

            server.serve();

        } catch(Exception e) {
            System.err.println(e.getMessage());
        }
    }
}
