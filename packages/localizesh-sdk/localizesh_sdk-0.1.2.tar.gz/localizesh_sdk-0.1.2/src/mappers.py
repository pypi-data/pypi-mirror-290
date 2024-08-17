import json
from .types import Document
from .protos.localize.segment_pb2 import Segment as ProtoSegment
from .protos.localize.document_pb2 import Document as ProtoDocument
from google.protobuf import struct_pb2


def from_proto_segment(proto_segment):
    segment = {'id': proto_segment.id,'text': proto_segment.text}

    if proto_segment.tags:
        tags = {tag_key: {'values': dict(attrs.values)} for tag_key, attrs in proto_segment.tags.items()}
        segment['tags'] = tags
    return segment

def from_proto_segments(proto_segments):
    return [from_proto_segment(proto_segment) for proto_segment in proto_segments]

def from_proto_document(proto_document):
    layout_dict = json.loads(proto_document.layout)
    metadata_dict = proto_document.metadata
    segments_list = from_proto_segments(proto_document.segments)
    document = Document(layout=layout_dict, segments=segments_list, metadata=metadata_dict)
    return document


def to_proto_segment(segment):
    proto_segment = ProtoSegment(id=segment['id'], text=segment['text'])
    if 'tags' in segment:
        for tag_key, attrs in segment['tags'].items():
            proto_segment.tags[tag_key].values.update(attrs['values'])
    return proto_segment

def to_proto_segments(segments):
    return [to_proto_segment(segment) for segment in segments]

def to_proto_document(document):
    proto_document = ProtoDocument(layout=json.dumps(document.layout))
    proto_document.segments.extend(to_proto_segments(document.segments))
    metadata = struct_pb2.Struct()
    metadata.update(document.metadata)
    proto_document.metadata.CopyFrom(metadata)
    return proto_document