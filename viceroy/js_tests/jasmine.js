describe("A suite", function() {
    console.log("RUNNING SUITE");
    it("contains spec with an expectation", function() {
        console.log("RAN SPEC 1");
        expect(true).toBe(true);
    });
    it("contains spec with an failing expectation", function() {
        console.log("RAN SPEC 2");
        expect(true).toBe(false);
    });
});
