test( "hello test", function() {
  console.log('running test 1');
  deepEqual( 1 , "1", "Failed!" );
});
test( "hello test", function() {
  console.log('running test 2');
  equal( 1 , "1", "Success!" );
});
console.log("TESTS LOADED");
